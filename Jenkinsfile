pipeline {
  agent {
    docker {
      image 'aunsiels/python3:latest'
    }

  }
  stages {
    stage('Build') {
      steps {
        echo 'Build Stage'
      }
    }
    stage('Test') {
      steps {
        sh 'make test-code'
      }
    }
  }
}