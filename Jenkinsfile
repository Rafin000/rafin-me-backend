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
                    // Assigning the image tag from the environment variable or defaulting to '1.0'
                    def imageTag = env.TAG ?: '1.0'
                    // Build the Docker image directly
                    sh "docker build -f Dockerfile -t ${DOCKER_IMAGE}:${imageTag} . || true"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    def imageTag = env.TAG ?: '1.0'
                    sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}:${imageTag}"
                }
            }
        }
    }

    post {
        always {
            script {
                def imageTag = env.TAG ?: '1.0'
                sh "docker rmi ${DOCKER_IMAGE}:${imageTag} || true"
                sh "rm requirements.txt || true"
            }
        }
        success {
            echo 'Build and push completed successfully!'
        }
        failure {
            echo 'Build or push failed.'
        }
    }
}
