pipeline {
   agent any
   stages {
        stage('Code analysis') {
            agent { 
                node {
                    label code 
                }
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
            steps {
                echo 'Building...'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
    }
}
