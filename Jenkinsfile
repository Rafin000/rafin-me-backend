pipeline {
    agent any

    // environment {
    //     DOCKER_IMAGE = 'rafin1998/rafin-blog-site:1.1'
    // }

    // parameters {
    //     string(name: 'DOCKER_USERNAME', defaultValue: 'rafin1998', description: 'Docker Hub Username')
    //     string(name: 'REPO_NAME', defaultValue: 'rafin-blog-site', description: 'Repository Name')
    //     string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Image Tag')
    // }

    environment {
        DOCKER_IMAGE = "${params.DOCKER_USERNAME}/${params.REPO_NAME}:${params.IMAGE_TAG}"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }
        stage('Install Poetry') {
            steps {
                sh 'curl -sSL https://install.python-poetry.org | python3 -'
                sh 'export PATH="$HOME/.local/bin:$PATH" && poetry --version'
            }
        }
        stage('Export Requirements') {
            steps {
                sh 'export PATH="$HOME/.local/bin:$PATH" && poetry export -f requirements.txt --output requirements.txt --without-hashes'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }
        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh "echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin"
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                sh "docker push ${DOCKER_IMAGE}"
            }
        }
    }
    post {
        always {
            echo 'Cleaning up...'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
