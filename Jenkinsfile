pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile'
    }

  }
  stages {
    stage('Build') {
      steps {
        echo 'Build Stage'
      }
    }
    stage('Test') {
      post {
        always {
          junit(allowEmptyResults: true, testResults: 'test-reports/results.xml')

        }

      }
      steps {
        sh 'make test-code-xml'
      }
    }
    stage('Static code metrics') {
      post {
        always {
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
      steps {
        echo 'Code Coverage'
        sh 'make test-coverage-xml'
        echo 'Style Check'
        sh 'make style-check'
        recordIssues(enabledForFailure: true, tool: pyLint(pattern: 'pylint_report.report'), sourceCodeEncoding: 'UTF-8')
      }
    }
  }
}
