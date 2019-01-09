pipeline {
  agent {
    docker {
      image 'aunsiels/python3:latest'
    }

  }
  stages {
    stage('Build') {
      steps {
        sh 'pip install --user -r requirements.txt'
      }
    }
    stage('Test') {
      steps {
        sh 'make test-code'
      }
    }
  }
}