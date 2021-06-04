pipeline {
   agent { label 'docker' }
   stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh "sleep 20"
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
    }
}
