pipeline {
    agent any // Run on Jenkins host, where docker is installed

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKER_IMAGE = 'rafin1998/rafin-blog-site'
        TAG = '0.7'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Rafin000/rafin-me-backend.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'make' // Run make without needing sudo
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = env.TAG ?: 'latest'
                    sh "docker build -t ${DOCKER_IMAGE}:${imageTag} ."
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
