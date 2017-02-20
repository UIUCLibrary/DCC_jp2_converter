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
            parallel linux: {
                node('all') {
                    deleteDir()
                    unstash "Source"
                    echo "Running Tox: Unit tests"
                    withEnv(["PATH=${env.PYTHON3}/..:${env.PATH}"]) {

                        echo "PATH = ${env.PATH}"
                        echo "Running: ${env.TOX}  --skip-missing-interpreters"
                        sh "${env.TOX}  --skip-missing-interpreters"
                        stash includes: "reports/*.xml", name: "Linux junit"
                    }
                }
                windows:
                {
                    node("Windows") {
                        deleteDir()
                        unstash "Source"
                        echo "Running Tox: Python 3.5 Unit tests"
                        bat "${env.TOX}  --skip-missing-interpreters"
                        stash includes: "reports/*.xml", name: "Windows junit"
                    }
                }
            }
        }
//        stage("Unit tests on Windows") {
//            agent {
//                label "Windows"
//            }
//
//            steps {
//                deleteDir()
//                unstash "Source"
//                echo "Running Tox: Python 3.5 Unit tests"
//                bat "${env.TOX}  --skip-missing-interpreters"
//
//            }
//            post {
//                always {
//                    stash includes: "reports/*.xml", name: "Windows junit"
//
//                }
//            }
//
//        }
        stage("flake8") {
            agent any

            steps {
                deleteDir()
                unstash "Source"
                echo "Running flake8 report"
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
        }


        stage("coverage") {
            agent any
            steps {
                deleteDir()
                unstash "Source"
                echo "Running Coverage report"
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
    }
    post {
        always {
            deleteDir()
            unstash "Linux junit"
            unstash "Windows junit"
            junit "reports/*.xml"
            echo "all done"
        }
    }
}
