#!groovy
node {
    stage('Pulling from Github'){
        checkout scm
        stash includes: '*', name: 'pysource'
    }
}



node {

    stage("Running Tox: Python 3.5 Unit tests"){
        env.PATH = "${env.PYTHON3}/..:${env.PATH}"
        unstash 'pysource'
        sh '$TOX -e py35'
        junit '**/junit-*.xml'


    }
}

parallel flake8: {
        echo "Running flake8 report"
        runTox("flake8", ".", 'flake8.html', "Flake8 Report")

    }, coverage: {
    echo "Running Coverage report"
    runTox("coverage", "htmlcov", 'index.html', "Coverage Report")
    }



parallel documentation: {
  node {
    echo 'Building documentation'
      try {
          stage("Generating Documentation for Archive"){
              unstash 'pysource'
              echo 'Creating virtualenv for generating docs'
              sh '$PYTHON3 -m virtualenv -p $PYTHON3 venv_doc'
              sh '. ./venv_doc/bin/activate && \
              pip install Sphinx && \
              python setup.py build_sphinx'

              dir('docs/build'){
                  stash includes: '**', name: 'sphinx_docs'
              }
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
}
sourceDist: {
    node{
        echo 'Building source distribution'
        stage("Building source distribution"){
            unstash 'pysource'
            sh '$PYTHON3 setup.py sdist'
            archiveArtifacts artifacts: 'dist/*.tar.gz'

        }
    }
  }

def runTox(environment, reportDir, reportFiles, reportName)
{
    stage("Running ${reportName}"){
      node {
        checkout scm
        git 'https://github.com/UIUCLibrary/DCC_jp2_converter.git'
        sh "${env.TOX} -e ${environment}"
        publishHTML([allowMissing: false,
                     alwaysLinkToLastBuild: false,
                     keepAll: false,
                     reportDir: "${reportDir}",
                     reportFiles: "${reportFiles}",
                     reportName: "${reportName}"])
      }

    }
}