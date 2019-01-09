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
        sh 'make test-code-xml'
      }
      post {
        always {
          // Archive unit tests for the future
          junit allowEmptyResults: true, testResults: 'test-reports/results.xml', fingerprint: true
        }
      }
    }
  }
}
