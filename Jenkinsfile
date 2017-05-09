#!groovy
pipeline {
    agent any

    stages {
        stage("Cloning Source") {
            agent any

            steps {
                deleteDir()
                echo "Cloning source"
                checkout scm
                stash includes: '**', name: "Source", useDefaultExcludes: false

            }

        }
        stage("Prepping 3rd party files") {
          steps{
            node(label: "!Windows"){
              deleteDir()
              sh "wget https://jenkins.library.illinois.edu/jenkins/userContent/binary/kdu_compress/kdu_compress.exe"
              sh "wget https://jenkins.library.illinois.edu/jenkins/userContent/binary/kdu_compress/kdu_v79R.dll"
              stash "kdu_compress"

            }
          }
        }

        stage("Unit tests") {
            steps {
                parallel(
                        "Windows": {
                            node(label: 'Windows') {
                                deleteDir()
                                unstash "Source"
                                echo "Running Tox: Python 3.5 Unit tests"
                                bat "${env.TOX}  --skip-missing-interpreters"
                                junit 'reports/junit-*.xml'

                            }
                        },
                        "Linux": {
                            node(label: "!Windows") {
                                deleteDir()
                                unstash "Source"
                                echo "Running Tox: Unit tests"
                                withEnv(["PATH=${env.PYTHON3}/..:${env.PATH}"]) {

                                    echo "PATH = ${env.PATH}"
                                    echo "Running: ${env.TOX}  --skip-missing-interpreters -e py35"
                                    sh "${env.TOX}  --skip-missing-interpreters -e py35"
                                }
                                junit 'reports/junit-*.xml'
                            }
                        }
                )
            }
        }

        stage("Static Analysis") {
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
                                  unstash "kdu_compress"
                                }
                                bat "${env.PYTHON3} cx_setup.py bdist_msi"
                                archiveArtifacts artifacts: "dist/**", fingerprint: true
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

            steps {
                deleteDir()
                script {
                    unstash "Documentation source"
                    sh("scp -r -i ${env.DCC_DOCS_KEY} docs/build/html/* ${env.DCC_DOCS_SERVER}/dcc_jp2_converter/")


                }


            }

        }
    }
}
