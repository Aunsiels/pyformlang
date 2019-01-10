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
          junit allowEmptyResults: true, testResults: 'test-reports/results.xml'
        }
      }
    }
    stage('Static code metrics') {
      steps {
        echo "Code Coverage"
        sh 'make test-coverage-xml'
        echo "Style Check"
        sh 'make style-check'
      }
      post{
        always{
          step([$class: 'CoberturaPublisher',
                         autoUpdateHealth: false,
                         autoUpdateStability: false,
                         coberturaReportFile: 'reports/coverage.xml',
                         failNoReports: false,
                         failUnhealthy: false,
                         failUnstable: false,
                         maxNumberOfBuilds: 10,
                         onlyStable: false,
                         sourceEncoding: 'ASCII',
                         zoomCoverageChart: false])
        }
      }
    }
  }
}
