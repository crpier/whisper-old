#!/usr/bin/env groovy

pipeline {
    agent any
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
