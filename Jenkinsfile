#!groovy
pipeline {
    agent any
    parameters {
      string(name: "PROJECT_NAME", defaultValue: "JP2 Converter", description: "Name given to the project")
      booleanParam(name: "UNIT_TESTS", defaultValue: true, description: "Run Automated Unit Tests")
      booleanParam(name: "STATIC_ANALYSIS", defaultValue: true, description: "Run static analysis tests")
      booleanParam(name: "PACKAGE", defaultValue: true, description: "Create a Packages")
      booleanParam(name: "DEPLOY", defaultValue: false, description: "Deploy SCCM")
      booleanParam(name: "BUILD_DOCS", defaultValue: true, description: "Build documentation")
      booleanParam(name: "UPDATE_DOCS", defaultValue: false, description: "Update the documentation")
      string(name: 'URL_SUBFOLDER', defaultValue: "dcc_jp2_converter", description: 'The directory that the docs should be saved under')

    }

    stages {
        stage("Cloning Source") {
            agent any

            steps {
                deleteDir()
                checkout scm
                stash includes: '**', name: "Source", useDefaultExcludes: false

            }

        }
        stage("Prepping 3rd party files") {
          steps{
            node(label: "!Windows"){
              deleteDir()
              sh "wget ${env.IMAGEMAGICK6_WIN_URL}"
              unzip dir: 'thirdparty/imagemagick', glob: '', zipFile: 'ImageMagick-6.9.8-6-portable-Q16-x64.zip'

              sh "wget ${env.EXIV2_WIN_URL}"
              unzip dir: 'thirdparty', glob: '', zipFile: 'exiv2.zip'

              sh "wget ${env.KDU_COMPRESS_WIN_URL}"
              unzip dir: 'thirdparty', glob: '', zipFile: 'kdu_v97_compress.zip'


              dir('thirdparty') {
                stash "thirdparty"
              }
            }
          }
        }

        stage("Unit tests") {
          when{
            expression{params.UNIT_TESTS == true}
          }
          steps {
              parallel(
                "Windows": {
                    node(label: 'Windows') {
                        deleteDir()
                        unstash "Source"
                        bat "${env.TOX}  --skip-missing-interpreters"
                        junit 'reports/junit-*.xml'

                    }
                },
                "Linux": {
                    node(label: "!Windows") {
                        deleteDir()
                        unstash "Source"
                        withEnv(["PATH=${env.PYTHON3}/..:${env.PATH}"]) {
                            sh "${env.TOX}  --skip-missing-interpreters -e py35"
                        }
                        junit 'reports/junit-*.xml'
                    }
                }
              )
          }
        }

        stage("Static Analysis") {
          when{
            expression{params.STATIC_ANALYSIS == true}
          }
          steps {
              parallel(
                  "flake8": {
                      node(label: "!Windows") {
                          deleteDir()
                          unstash "Source"
                          sh "${env.TOX} -e flake8"
                          publishHTML target: [
                                  allowMissing         : false,
                                  alwaysLinkToLastBuild: false,
                                  keepAll              : true,
                                  reportDir            : "reports",
                                  reportFiles          : "flake8.html",
                                  reportName           : "Flake8 Report"
                          ]
                      }
                  },
                  "coverage": {
                      node(label: "!Windows") {
                          deleteDir()
                          unstash "Source"
                          sh "${env.TOX} -e coverage"
                          publishHTML target: [
                                  allowMissing         : false,
                                  alwaysLinkToLastBuild: false,
                                  keepAll              : true,
                                  reportDir            : "reports/coverage",
                                  reportFiles          : "index.html",
                                  reportName           : "Coverage Report"
                          ]
                      }
                  }
              )
            }

        }

        stage("Documentation") {
            agent any
            when{
              expression{params.BUILD_DOCS == true}
            }
            steps {
                deleteDir()
                unstash "Source"
                withEnv(['PYTHON=${env.PYTHON3}']) {
                    dir('docs') {
                        sh 'make html SPHINXBUILD=$SPHINXBUILD'
                    }
                    stash includes: '**', name: "Documentation source", useDefaultExcludes: false
                }
            }
            post {
                success {
                    sh 'tar -czvf sphinx_html_docs.tar.gz -C docs/build/html .'
                    archiveArtifacts artifacts: 'sphinx_html_docs.tar.gz'
                }
            }
        }

        stage("Packaging") {
          when{
            expression{params.PACKAGE == true}
          }
          steps {
            parallel(
              "Windows Wheel": {
                  node(label: "Windows") {
                      deleteDir()
                      unstash "Source"
                      bat "${env.PYTHON3} setup.py bdist_wheel --universal"
                      archiveArtifacts artifacts: "dist/**", fingerprint: true
                  }
              },
              "Windows CX_Freeze MSI": {
                  node(label: "Windows") {
                      deleteDir()
                      unstash "Source"
                      dir("dcc_jp2_converter/thirdparty"){
                        unstash "thirdparty"
                      }
                      bat """ ${env.PYTHON3} -m venv .env
                              call .env/Scripts/activate.bat
                              pip install -r requirements.txt
                              ${env.PYTHON3} cx_setup.py bdist_msi --add-to-path=true
                              """

                      dir("dist"){
                        stash includes: "*.msi", name: "msi"
                      }

                  }
                  node(label: "Windows") {
                    deleteDir()
                    git url: 'https://github.com/UIUCLibrary/ValidateMSI.git'
                    unstash "msi"
                    // validate_msi.py

                    bat """
                      ${env.PYTHON3} -m venv .env
                      call .env/Scripts/activate.bat
                      pip install setuptools --upgrade
                      pip install -r requirements.txt
                      python setup.py install

                      echo Validating msi file(s)
                      FOR /f "delims=" %%A IN ('dir /b /s *.msi') DO (
                        python validate_msi.py ^"%%A^" frozen.yml
                        if not %errorlevel%==0 (
                          echo errorlevel=%errorlevel%
                          exit /b %errorlevel%
                          )
                        )
                      """
                  archiveArtifacts artifacts: "*.msi", fingerprint: true
                  }
              },
              "Source Release": {
                  deleteDir()
                  unstash "Source"
                  sh "${env.PYTHON3} setup.py sdist"
                  archiveArtifacts artifacts: "dist/**", fingerprint: true
              }
            )
          }
        }
        stage("Update online documentation") {
            agent any
            when{
              expression{params.UPDATE_DOCS == true && params.BUILD_DOCS == true}
            }

            steps {
                deleteDir()
                script {
                    echo "Updating online documentation"
                    unstash "Documentation source"
                    try {
                      sh("rsync -rv -e \"ssh -i ${env.DCC_DOCS_KEY}\" docs/build/html/ ${env.DCC_DOCS_SERVER}/${params.URL_SUBFOLDER}/ --delete")
                    } catch(error) {
                      echo "Error with uploading docs"
                      throw error
                    }
                }
            }
        }
        stage("Deploy - Staging"){
          agent any
          when {
            expression{params.DEPLOY == true && params.PACKAGE == true}
          }
          steps {
            deleteDir()
            unstash "msi"
            sh "rsync -rv ./ \"${env.SCCM_STAGING_FOLDER}/${params.PROJECT_NAME}/\""
            input("Deploy to production?")
          }
        }

        stage("Deploy - SCCM upload"){
          agent any
          when {
            expression{params.DEPLOY == true && params.PACKAGE == true}
          }
          steps {
            deleteDir()
            unstash "msi"
            sh "rsync -rv ./ ${env.SCCM_UPLOAD_FOLDER}/"
          }
        }
    }
}
