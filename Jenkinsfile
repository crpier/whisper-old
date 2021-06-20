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
               label 'code'
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
               stage('Test') {
                   agent { 
                       // TODO create testing image
                       label 'code'
                   }
                   steps {
                       echo 'Testing...'
                   }
               }
               stage('CI: Build') {
                   steps {
                       script {
                           // dockerImage = docker.build "tiannaru/whisper:${env.BRANCH_NAME}"
                           // docker.withRegistry('https://registry.hub.docker.com', 'dockerHub') {
                           //     dockerImage.push()
                           // }
                           echo "lgtm"
                       }
                   }
               }
           }
       }
    }
}
