pipeline {
   agent any
   stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
        stage('Code analysis') {
            agent { 
                label code 
            }
            stages {
                stage('Code analysis: pylint') {
                    steps {
                        sh "pylint --fail-under=4 src"
                    }
                }
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
    }
}
