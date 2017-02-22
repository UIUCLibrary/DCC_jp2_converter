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

                echo 'Building documentation'
                echo 'Creating virtualenv for generating docs'
                sh "${env.PYTHON3} -m virtualenv -p ${env.PYTHON3} venv_doc"
                withEnv(['PYTHON=${env.PYTHON3}']) {
//
//                    sh 'make docs'
                    sh "$SPHINXBUILD 'docs/source' 'docs/build/html' html"
//                    @$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
                }
//                }docs
//                sh '. ./venv_doc/bin/activate && \
//                          pip install Sphinx==1.5.1 && \
//                          make clean && \
//                          make docs'
//                          python setup.py build_sphinx'
                stash includes: '**', name: "Documentation source", useDefaultExcludes: false
                echo "running git dif end"


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
                            script: "git diff --quiet --exit-code docs/build/html/",
                            returnStatus: true
                    )

                    if (dif != "0") {
                        echo "Online documentation is different than what was generated"
//                        input 'Update documentation?'
//                        sh "git commit -m 'Build new documentation' -- docs/build/html"
//                        sh "git push origin master"
                    } else {
                        echo 'No new documentation found'
                    }

                }


            }

        }
    }
}
