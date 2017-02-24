#!groovy
pipeline {
    agent any

    stages {
        stage("Cloning Source") {
            agent any

            steps {
                deleteDir()
                echo "Cloning source"
//                checkout scm
                git credentialsId: 'ccb29ea2-6d0f-4bfa-926d-6b4edd8995a8', url: 'https://github.com/UIUCLibrary/DCC_jp2_converter.git'
                stash includes: '**', name: "Source", useDefaultExcludes: false

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
                    def dif = sh(
                            script: "git diff --exit-code docs/build/html/",
                            returnStatus: true
                    )

                    if (dif != "0") {
                        echo "Online documentation is different than what was generated"
//                        input 'Update documentation?'
                        withCredentials([[$class          : 'UsernamePasswordMultiBinding',
                                          credentialsId   : 'ccb29ea2-6d0f-4bfa-926d-6b4edd8995a8',
                                          usernameVariable: 'GIT_USERNAME',
                                          passwordVariable: 'GIT_PASSWORD']]) {

                            sh "git commit -m 'Build new documentation' -- docs/build/html"
//                        sh "git remote set-url origin https://github.com/UIUCLibrary/DCC_jp2_converter.git"
//                            sh "git push"
//                            sh("git tag -a some_tag -m 'Jenkins'")
//                            sh('git push https://${GIT_USERNAME}:${GIT_PASSWORD}@<REPO> --tags')
                        }
//                        sh "git push origin master"
                    } else {
                        echo 'No new documentation found'
                    }

                }


            }

        }
    }
}
