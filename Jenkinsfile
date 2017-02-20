#!groovy
pipeline {
    agent none

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
        stage("Unit tests on Linux") {
            agent any
            steps {
                deleteDir()
                unstash "Source"
                echo "Running Tox: Unit tests"
                sh "${env.TOX}  --skip-missing-interpreters"

            }
        }
        stage("Unit tests on Windows") {
            agent {
                label "Windows"
            }

            steps {
                unstash "Source"
                steps {
                    deleteDir()
                    unstash "Source"
                    echo "Running Tox: Python 3.5 Unit tests"
                    bat "${env.TOX}  --skip-missing-interpreters"
                }
            }

        }
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
                publishHTML([allowMissing         : false,
                             alwaysLinkToLastBuild: false,
                             keepAll              : false,
                             reportDir            : "reports/coverage",
                             reportFiles          : "index.html",
                             reportName           : "Coverage Report"])

//                runTox("coverage", "reports/coverage", 'index.html', "Coverage Report")
            }
        }

        stage("Documentation") {
            agent any

            steps {
                deleteDir()
                unstash "Source"
                echo 'Building documentation'
//                try {
                echo 'Creating virtualenv for generating docs'
                sh "${env.PYTHON3} -m virtualenv -p ${env.PYTHON3} venv_doc"
                sh '. ./venv_doc/bin/activate && \
                          pip install Sphinx && \
                          python setup.py build_sphinx'

                dir('docs/build') {
                    stash includes: '**', name: 'sphinx_docs'
                }
                sh 'tar -czvf sphinx_docs.tar.gz html'
                archiveArtifacts artifacts: 'sphinx_docs.tar.gz'
                dir('docs') {
                    sh 'make clean'
                }
//                } catch (error) {
//                    echo 'Unable to generate Sphinx documentation'
            }
        }
    }
}
//        stage("Archiving source distribution") {
//            echo 'Building source distribution'
//            sh '$PYTHON3 setup.py sdist --formats=gztar,zip'
//            archiveArtifacts artifacts: 'dist/*.tar.gz'
//            archiveArtifacts artifacts: 'dist/*.zip'

//}
//}

//}

//node {
//
//
//    try {
//        stage("Unit tests") {
//            echo "Running Tox: Python 3.5 Unit tests"
//            env.PATH = "${env.PYTHON3}/..:${env.PATH}"
//            sh '$TOX -e py35'
//        }
//
//        stage("flake8") {
//            echo "Running flake8 report"
//            sh "${env.TOX} -e flake8"
//        }
//
//        stage("coverage") {
//            echo "Running Coverage report"
//            runTox("coverage", "reports/coverage", 'index.html', "Coverage Report")
//
//        }
//
//        stage("Documentation") {
//            echo 'Building documentation'
//            try {
//                echo 'Creating virtualenv for generating docs'
//                sh '$PYTHON3 -m virtualenv -p $PYTHON3 venv_doc'
//                sh '. ./venv_doc/bin/activate && \
//              pip install Sphinx && \
//              python setup.py build_sphinx'
//
//                dir('docs/build') {
//                    stash includes: '**', name: 'sphinx_docs'
//                }
//                sh 'tar -czvf sphinx_docs.tar.gz html'
//                archiveArtifacts artifacts: 'sphinx_docs.tar.gz'
//                dir('docs') {
//                    sh 'make clean'
//                }
//            } catch (error) {
//                echo 'Unable to generate Sphinx documentation'
//            }
//        }
//
//        stage("Archiving source distribution") {
//            echo 'Building source distribution'
//            sh '$PYTHON3 setup.py sdist --formats=gztar,zip'
//            archiveArtifacts artifacts: 'dist/*.tar.gz'
//            archiveArtifacts artifacts: 'dist/*.zip'
//
//        }
//    } finally {
//        junit '**/reports/junit-*.xml'
//
//        withEnv(['PYTHON=$PYTHON3']) {
//            try {
//                echo "Running clean"
//                sh 'make clean'
//            } catch (error) {
//                echo "WARNING: Unable to fully clean."
//            }
//
//        }
//    }
//
//}
//
//
//def runTox(environment, reportDir, reportFiles, reportName) {
//    sh "${env.TOX} -e ${environment}"
//    publishHTML([allowMissing         : false,
//                 alwaysLinkToLastBuild: false,
//                 keepAll              : false,
//                 reportDir            : "${reportDir}",
//                 reportFiles          : "${reportFiles}",
//                 reportName           : "${reportName}"])
//
//}
