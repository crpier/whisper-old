pipeline {
   agent none
   stages {
        stage('Code analysis') {
            agent { 
                label 'code'
            }
            stages {
                stage('Code analysis: checkout') {
                   steps {
                       checkout scm
                   }
                }
                stage('Code analysis: pylint') {
                    steps {
                        sh "pylint"
                    }
                }
            }
        }
        stage('Build') {
            agent { 
                label 'code'
            }
            steps {
                echo 'Building...'
            }
        }
        stage('Test') {
            agent { 
                label 'code'
            }
            steps {
                echo 'Testing...'
            }
        }
    }
}
