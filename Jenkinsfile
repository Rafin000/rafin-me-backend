pipeline {
    agent any

    environment {
        DOCKER_USERNAME = "rafin1998"
        REPO_NAME = "rafin-blog-site"
        GIT_USER_NAME = "Rafin000"
        GIT_REPO_NAME = "rafin-me-backend"
        GIT_DEPLOYMENT_REPO_NAME = "rafin-blog-site-deployment"
        GIT_USER_EMAIL = "marufulislam00000@gmail.com"
    }

    stages {
        stage('Checkout and Get Version') {
            steps {
                script {
                    git branch: 'main', url: "https://github.com/${GIT_USER_NAME}/${GIT_REPO_NAME}.git"

                    writeFile file: 'get_version.sh', text: '''#!/bin/bash
                        GITHUB_TOKEN=$1  
                        FILE_PATH="k8s-backend/backend-depl.yaml"
                        REPO_URL="https://raw.githubusercontent.com/${GIT_USER_NAME}/${GIT_DEPLOYMENT_REPO_NAME}/main/${FILE_PATH}"

                        content=$(curl -s -H "Authorization: token ${GITHUB_TOKEN}" ${REPO_URL})
                        current_tag=$(echo "$content" | grep -o 'image: [^ ]*' | grep -o '[0-9]\\+\\.[0-9]')
                        current_tag="${current_tag:-0.0}"

                        IFS='.' read -r major minor <<< "$current_tag"
                        minor=$((minor + 1))
                        if [ "$minor" -ge 10 ]; then
                            major=$((major + 1))
                            minor=0
                        fi
                        echo "${major}.${minor}"
                    '''
                    sh 'chmod +x get_version.sh'

                    withCredentials([string(credentialsId: 'github', variable: 'GITHUB_TOKEN')]) {
                        env.IMAGE_TAG = sh(script: './get_version.sh ${GITHUB_TOKEN}', returnStdout: true).trim()
                    }
                    env.DOCKER_IMAGE = "${DOCKER_USERNAME}/${REPO_NAME}:${IMAGE_TAG}"
                    echo "New version: ${IMAGE_TAG}, Docker image: ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Install Poetry') {
            steps {
                sh '''
                    curl -sSL https://install.python-poetry.org | python3 -
                    export PATH="$HOME/.local/bin:$PATH"
                    echo "PATH: $PATH"
                    poetry --version
                '''
            }
        }

        stage('Export Requirements') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    poetry export -f requirements.txt --output requirements.txt --without-hashes
                '''
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

        stage('Update Deployment File') {
            steps {
                withCredentials([string(credentialsId: 'github', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                        if [ -d "${GIT_REPO_NAME}" ]; then
                            rm -rf ${GIT_REPO_NAME}
                        fi

                        git clone https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_DEPLOYMENT_REPO_NAME}.git
                        cd ${GIT_DEPLOYMENT_REPO_NAME}
                        
                        git config user.name "${GIT_USER_NAME}"
                        git config user.email "${GIT_USER_EMAIL}"

                        sed -i "s|image: ${DOCKER_USERNAME}/${REPO_NAME}:[^ ]*|image: ${DOCKER_IMAGE}|g" k8s-backend/backend-depl.yaml
                        git add k8s-backend/backend-depl.yaml
                        git commit -m "Update deployment image to ${IMAGE_TAG}"
                        git push https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_DEPLOYMENT_REPO_NAME}.git
                    '''
                }
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
