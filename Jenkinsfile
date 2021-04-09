#!/usr/bin/env groovy

pipeline {

    agent {
        docker {
            image 'python'
            args '-u root'
        }
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
