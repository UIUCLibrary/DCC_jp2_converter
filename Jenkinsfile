#!groovy
node {
  checkout scm
  withEnv(['PYTHON=${env.PYTHON3}']) {
      sh 'make clean'
  }

  try {
    stage("Running Tox: Python 3.5 Unit tests"){
        env.PATH = "${env.PYTHON3}/..:${env.PATH}"
        sh '$TOX -e py35'
      }

    stage("flake8"){
      echo "Running flake8 report"
      runTox("flake8", "reports", 'flake8.html', "Flake8 Report")
    }

    stage("coverage"){
      echo "Running Coverage report"
      runTox("coverage", "reports/coverage", 'index.html', "Coverage Report")

    }

    stage("Documentation"){
      echo 'Building documentation'
      try {
              echo 'Creating virtualenv for generating docs'
              sh '$PYTHON3 -m virtualenv -p $PYTHON3 venv_doc'
              sh '. ./venv_doc/bin/activate && \
              pip install Sphinx && \
              python setup.py build_sphinx'

              dir('docs/build'){
                  stash includes: '**', name: 'sphinx_docs'
          }

          stage("Archiving Documentation"){
              unstash 'sphinx_docs'
              sh 'tar -czvf sphinx_docs.tar.gz html'
              archiveArtifacts artifacts: 'sphinx_docs.tar.gz'
          }



      } catch(error) {
          echo 'Unable to generate Sphinx documentation'
      }
    }

    stage("Building source distribution"){
      echo 'Building source distribution'
        sh '$PYTHON3 setup.py sdist'
        archiveArtifacts artifacts: 'dist/*.tar.gz'

    }
  } finally {
    junit '**/reports/junit-*.xml'
  }

}


def runTox(environment, reportDir, reportFiles, reportName)
{
      sh "${env.TOX} -e ${environment}"
      publishHTML([allowMissing: false,
                   alwaysLinkToLastBuild: false,
                   keepAll: false,
                   reportDir: "${reportDir}",
                   reportFiles: "${reportFiles}",
                   reportName: "${reportName}"])

}
