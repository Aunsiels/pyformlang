pipeline {
  agent {
    docker {
      image 'python:3.6'
    }

  }
  stages {
    stage('Build') {
      steps {
        sh '''virtualenv -p /usr/bin/python3.6 venv
'''
        sh 'source venv/bin/activate'
        sh 'pip3 install -r requirements.txt'
      }
    }
    stage('Test') {
      steps {
        sh 'make test-code'
      }
    }
  }
}