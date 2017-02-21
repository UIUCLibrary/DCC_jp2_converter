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
                stash includes: '**', name: "Source"

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
                                                        reportDir            : "reports/cov_html",
                                                        reportFiles          : "index.html",
                                                        reportName           : "Coverage Report"
                                                ]
                                            }
                                        }
                                )
                            }
                        }
                )
            }
        }
//        stage("flake8") {
//            agent any
//
//            steps {
//                deleteDir()
//                unstash "Source"
//                echo "Running flake8 report"
//                sh "${env.TOX} -e flake8"
//
//                publishHTML target: [
//                        allowMissing         : false,
//                        alwaysLinkToLastBuild: false,
//                        keepAll              : true,
//                        reportDir            : "reports",
//                        reportFiles          : "flake8.html",
//                        reportName           : "Flake8 Report"
//                ]
//
//            }
//        }


//        stage("coverage") {
//            agent any
//            steps {
//                deleteDir()
//                unstash "Source"
//                echo "Running Coverage report"
//                sh "${env.TOX} -e coverage"
//                publishHTML target: [
//                        allowMissing         : false,
//                        alwaysLinkToLastBuild: false,
//                        keepAll              : true,
//                        reportDir            : "reports/coverage",
//                        reportFiles          : "index.html",
//                        reportName           : "Coverage Report"
//                ]
//
//            }
//        }

        stage("Documentation") {
            agent any

            steps {
                deleteDir()
                unstash "Source"
                echo 'Building documentation'
                echo 'Creating virtualenv for generating docs'
                sh "${env.PYTHON3} -m virtualenv -p ${env.PYTHON3} venv_doc"
                sh '. ./venv_doc/bin/activate && \
                          pip install Sphinx && \
                          python setup.py build_sphinx'

                sh 'tar -czvf sphinx_docs.tar.gz docs/build/html'
                stash includes: 'docs/build/**', name: 'sphinx_docs'
                archiveArtifacts artifacts: 'sphinx_docs.tar.gz'
            }
        }

        stage("Packaging source") {
            agent any

            steps {
                deleteDir()
                unstash "Source"
                sh "${env.PYTHON3} setup.py sdist"
            }

            post {
                success {
                    archiveArtifacts artifacts: "dist/**", fingerprint: true
                }
            }

        }

        stage("Packaging Windows binary Wheel") {
            agent {
                label "Windows"
            }

            steps {
                deleteDir()
                unstash "Source"
                bat "${env.PYTHON3} setup.py bdist_wheel --universal"
            }
            post {
                success {
                    archiveArtifacts artifacts: "dist/**", fingerprint: true
                }
            }

        }
    }

    post {
        always {
            deleteDir()
//            unstash "Linux junit"
//            unstash "Windows junit"
//            junit "reports/*.xml"
            echo "all done"
        }
    }
}
