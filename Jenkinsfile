pipeline {
  agent {
    docker {
      image 'python:3.6'
    }

  }
  stages {
    stage('Test') {
      steps {
        sh 'pip3 install -r requirements.txt'
        sh 'make test-code'
      }
    }
  }
}