pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Install Poetry') {
            steps {
                script {
                    sh '''
                        curl -sSL https://install.python-poetry.org | python3 -
                        export PATH="/var/lib/jenkins/.local/bin:$PATH"
                        echo $PATH
                        poetry --version
                    '''
                }
            }
        }

        stage('Export Requirements') {
            steps {
                script {
                    sh '''
                        export PATH="/var/lib/jenkins/.local/bin:$PATH"
                        poetry export -f requirements.txt --output requirements.txt --without-hashes
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = env.TAG ?: 'latest'
                    sh "make image TAG=${imageTag}"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}:${TAG}"
                }
            }
        }
    }

    post {
        always {
            sh "docker rmi ${DOCKER_IMAGE}:${TAG} || true"
        }
        success {
            echo 'Build and push completed successfully!'
        }
        failure {
            echo 'Build or push failed.'
        }
    }
}
