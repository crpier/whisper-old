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
                stage('Code analysis: check') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                            sh "pylint --fail-under=4 src"
                            sh "flake8 src"
                            sh "pydocstyle src"
                        }
                    }
                }
            }
        }
        stage('Build') {
            agent { 
                label 'code'
            }
            steps {
                script {
                    dockerImage = docker.build 'tiannaru/whisper:latest'
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerHub') {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Test') {
            agent { 
                // TODO create testing image
                label 'code'
            }
            steps {
                echo 'Testing...'
            }
        }
   }
}
