pipeline {
  agent {
    docker {
      image 'aunsiels/python3:latest'
    }

  }
  stages {
    stage('Build') {
      steps {
        sh 'virtualenv -p /usr/bin/python3.6 venv'
        sh 'source venv/bin/activate'
        sh 'pip3 install --user -r requirements.txt'
      }
    }
    stage('Test') {
      steps {
        sh 'make test-code'
      }
    }
  }
}