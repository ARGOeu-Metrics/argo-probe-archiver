pipeline {
    agent any
    options {
        checkoutToSubdirectory('argo-probe-archiver')
    }
    environment {
        PROJECT_DIR="argo-probe-archiver"
        GIT_COMMIT=sh(script: "cd ${WORKSPACE}/$PROJECT_DIR && git log -1 --format=\"%H\"",returnStdout: true).trim()
        GIT_COMMIT_HASH=sh(script: "cd ${WORKSPACE}/$PROJECT_DIR && git log -1 --format=\"%H\" | cut -c1-7",returnStdout: true).trim()
        GIT_COMMIT_DATE=sh(script: "date -d \"\$(cd ${WORKSPACE}/$PROJECT_DIR && git show -s --format=%ci ${GIT_COMMIT_HASH})\" \"+%Y%m%d%H%M%S\"",returnStdout: true).trim()

    }
    stages {
        stage ('Build Rocky 9 RPM') {
            agent {
                docker {
                    image 'argo.registry:5000/epel-9-ams'
                    args '-u jenkins:jenkins'
                }
            }
            steps {
                echo 'Building Rpm...'
                withCredentials(bindings: [sshUserPrivateKey(credentialsId: 'jenkins-rpm-repo', usernameVariable: 'REPOUSER', \
                                                            keyFileVariable: 'REPOKEY')]) {
                    sh "/home/jenkins/build-rpm.sh -w ${WORKSPACE} -b ${BRANCH_NAME} -d rocky9 -p ${PROJECT_DIR} -s ${REPOKEY}"
                }
                archiveArtifacts artifacts: '**/*.rpm', fingerprint: true
            }
            post {
                always {
                    cleanWs()
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        success {
            script{
                if ( env.BRANCH_NAME == 'master' || env.BRANCH_NAME == 'devel' ) {
                    slackSend( message: ":rocket: New version for <$BUILD_URL|$PROJECT_DIR>:$BRANCH_NAME Job: $JOB_NAME !")
                }
            }
        }
        failure {
            script{
                if ( env.BRANCH_NAME == 'master' || env.BRANCH_NAME == 'devel' ) {
                    slackSend( message: ":rain_cloud: Build Failed for <$BUILD_URL|$PROJECT_DIR>:$BRANCH_NAME Job: $JOB_NAME")
                }
            }
        }
    }
}
