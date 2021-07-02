def get_tag(String branch_name) {
    if (branch_name == 'main') {
        tag=latest
    } else {
        tag=staging
    }
    return tag
}

pipeline {
   agent none
   stages {
       stage('CI') {
           agent { 
               label 'ci-python'
           }
           stages {
               stage('CI: Checkout') {
                   steps {
                       checkout scm
                   }
               }
               stage('CI: Linting') {
                   steps {
                       catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                           sh "pylint --fail-under=4 src"
                               sh "flake8 src"
                               sh "pydocstyle src"
                       }
                   }
               }
               stage('CI: Unit Test') {
                   steps {
                       echo 'Testing...'
                   }
               }
           }
       }
       stage('CD') {
           agent {
               label 'cd'
           }
           stages {
               stage('CD: Build') {
                   steps {
                       script {
                           dockerImage = docker.build "tiannaru/whisper:${env.BRANCH_NAME}"
                       }
                   }
               }
               stage('CD: Push') {
                   steps {
                       script {
                           // docker.withRegistry('https://registry.hub.docker.com', 'dockerHub') {
                           //     dockerImage.push()
                           // }
                           echo 'Looks good for now'
                       }
                   }
               }
           }
       }
   }
}
