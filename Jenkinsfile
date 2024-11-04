pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKER_IMAGE = 'rafin1998/rafin-blog-site'
        TAG = '0.7' // Update the tag as needed
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Rafin000/rafin-me-backend.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Install make if it's not available
                sh 'which make || sudo apt update && sudo apt install -y make'
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
