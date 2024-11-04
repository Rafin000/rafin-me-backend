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

        stage('Install Poetry') {
            steps {
                script {
                    // Install Poetry
                    sh 'curl -sSL https://install.python-poetry.org | python3 -'
                    // Add Poetry to the PATH
                    sh 'export PATH="$HOME/.local/bin:$PATH"'
                }
            }
        }

        stage('Export Requirements') {
            steps {
                script {
                    // Export Python dependencies to requirements.txt
                    sh 'poetry export -f requirements.txt --output requirements.txt --without-hashes'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = env.TAG ?: 'latest'
                    // Build the Docker image directly
                    sh "docker build -f Dockerfile -t ${DOCKER_IMAGE}:${imageTag} . || true"
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
            sh "rm requirements.txt || true"
        }
        success {
            echo 'Build and push completed successfully!'
        }
        failure {
            echo 'Build or push failed.'
        }
    }
}
