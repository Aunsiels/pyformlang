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
        sh 'make test-code-xml || echo 0'
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
        sh 'PYLINTHOME=. pylint pyformlang > pylint.report || true'
        sh 'pycodestyle pyformlang > pep8.report || true'
        recordIssues(enabledForFailure: true, tool: pyLint(pattern: 'pylint.report'), sourceCodeEncoding: 'UTF-8')
        recordIssues(enabledForFailure: true, tool: pep8(pattern: 'pep8.report'), sourceCodeEncoding: 'UTF-8')
      }
    }
  }
}
