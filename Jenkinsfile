pipeline {
  agent {
    docker {
      image 'aunsiels/python3:latest'
    }

  }
  stages {
    stage('Build') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }
    stage('Test') {
      steps {
        sh 'make test-code'
      }
    }
  }
}