pipeline {
   agent { label 'build-label' }
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
