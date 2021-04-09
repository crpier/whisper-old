#!/usr/bin/env groovy

pipeline {

    agent {
        docker{ image 'python' }
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'pip install -r req.txt'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'python -m pytest'
            }
        }
    }
}
