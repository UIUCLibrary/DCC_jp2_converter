#!groovy
@Library("ds-utils")
import org.ds.*
pipeline {
    agent any
    environment {
        mypy_args = "--junit-xml=mypy.xml"
        pytest_args = "--junitxml=reports/junit-{env:OS:UNKNOWN_OS}-{envname}.xml --junit-prefix={env:OS:UNKNOWN_OS}  --basetemp={envtmpdir}"
    }
    parameters {
        string(name: "PROJECT_NAME", defaultValue: "JP2 Converter", description: "Name given to the project")
        booleanParam(name: "UNIT_TESTS", defaultValue: true, description: "Run Automated Unit Tests")
        booleanParam(name: "ADDITIONAL_TESTS", defaultValue: true, description: "Run additional tests")
        booleanParam(name: "PACKAGE", defaultValue: true, description: "Create a Packages")
        booleanParam(name: "DEPLOY", defaultValue: false, description: "Deploy SCCM")
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
            steps {
                node(label: "!Windows") {
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
            when {
                expression { params.UNIT_TESTS == true }
            }
            steps {
                parallel(
                        "Windows": {
                            script {
                                def runner = new Tox(this)
                                runner.env = "pytest"
                                runner.windows = true
                                runner.stash = "Source"
                                runner.label = "Windows"
                                runner.post = {
                                    junit 'reports/junit-*.xml'
                                }
                                runner.run()
                            }
                        },
                        "Linux": {
                            script {
                                def runner = new Tox(this)
                                runner.env = "pytest"
                                runner.windows = false
                                runner.stash = "Source"
                                runner.label = "!Windows"
                                runner.post = {
                                    junit 'reports/junit-*.xml'
                                }
                                runner.run()
                            }
                        }
                )
            }
        }

        stage("Additional tests") {
            when {
                expression { params.ADDITIONAL_TESTS == true }
            }

            steps {
                parallel(
                        "Documentation": {
                            script {
                                def runner = new Tox(this)
                                runner.env = "docs"
                                runner.windows = false
                                runner.stash = "Source"
                                runner.label = "!Windows"
                                runner.post = {
                                    dir('.tox/dist/html/') {
                                        stash includes: '**', name: "HTML Documentation", useDefaultExcludes: false
                                    }
                                }
                                runner.run()

                            }
                        },
//                        "MyPy": {
//                            script {
//                                def runner = new Tox(this)
//                                runner.env = "mypy"
//                                runner.windows = false
//                                runner.stash = "Source"
//                                runner.label = "!Windows"
//                                runner.post = {
//                                    junit 'mypy.xml'
//                                }
//                                runner.run()
//
//                            }
//                        },
                        "flake8": {
                            node(label: "Linux") {
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
                            node(label: "Linux") {
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

        stage("Packaging") {
            when {
                expression { params.PACKAGE == true || params.DEPLOY == true }
            }
            steps {
                parallel(
                        "Windows Wheel": {
                            node(label: "Windows") {
                                deleteDir()
                                unstash "Source"
                                bat "${tool 'Python3.6.3_Win64'} setup.py bdist_wheel"
                                archiveArtifacts artifacts: "dist/**", fingerprint: true
                            }
                        },
                        "Windows CX_Freeze MSI": {
                            node(label: "Windows") {
                                deleteDir()
                                unstash "Source"
                                dir("dcc_jp2_converter/thirdparty") {
                                    unstash "thirdparty"
                                }
                                bat """ ${tool 'Python3.6.3_Win64'} -m venv venv
                              call venv/Scripts/activate.bat
                              pip install -r requirements.txt
                              ${tool 'Python3.6.3_Win64'} cx_setup.py bdist_msi --add-to-path=true
                              """

                                dir("dist") {
                                    stash includes: "*.msi", name: "msi"
                                }

                            }
                            node(label: "Windows") {
                                deleteDir()
                                git url: 'https://github.com/UIUCLibrary/ValidateMSI.git'
                                unstash "msi"
                                // validate_msi.py

                                bat """
                      ${tool 'Python3.6.3_Win64'} -m venv .env
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
                            createSourceRelease(env.PYTHON3, "Source")
                        }
                )
            }
        }
        stage("Deploy - Staging") {
            agent any
            when {
                expression { params.DEPLOY == true }
            }
            steps {
                deployStash("msi", "${env.SCCM_STAGING_FOLDER}/${params.PROJECT_NAME}/")
                input("Deploy to production?")
            }
        }

        stage("Deploy - SCCM upload") {
            agent any
            when {
                expression { params.DEPLOY == true }
            }
            steps {
                deployStash("msi", "${env.SCCM_UPLOAD_FOLDER}")
            }
            post {
                success {
                    script{
                        unstash "Source"
                        def  deployment_request = requestDeploy this, "deployment.yml"
                        echo deployment_request
                        writeFile file: "deployment_request.txt", text: deployment_request
                        archiveArtifacts artifacts: "deployment_request.txt"
                    }

                }
            }
        }
        stage("Update online documentation") {
            agent any
            when {
                expression {params.UPDATE_DOCS == true }
            }

            steps {
                updateOnlineDocs url_subdomain: params.URL_SUBFOLDER, stash_name: "HTML Documentation"
            }
        }

    }
}
