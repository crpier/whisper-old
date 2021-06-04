pipeline {
   agent any
   stages {
        stage('Code analysis') {
            agent { 
                dockerfile {
                    filename 'code.Dockerfile'
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
