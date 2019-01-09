pipeline {
  agent {
    docker {
      image 'python:3.6'
    }

  }
  stages {
    stage('Test') {
      steps {
        sh 'make test-code'
      }
    }
  }
}