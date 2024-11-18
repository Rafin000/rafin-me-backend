pipeline {
    agent any

    environment {
        DOCKER_USERNAME = "rafin1998"
        REPO_NAME = "rafin-blog-site"
        GIT_USER_NAME = "Rafin000"
        GIT_USER_EMAIL = "marufulislam00000@gmail.com"
        GIT_REPO_NAME = "rafin-me-backend"
        DEPLOYMENT_FILE = "k8s/backend-depl.yaml"
    }

    stages {
        stage('Checkout and Get Version') {
            steps {
                script {
                    git branch: 'main', url: "https://github.com/${GIT_USER_NAME}/${GIT_REPO_NAME}.git"
                    
                    writeFile file: 'get_version.sh', text: '''#!/bin/bash
                        GIT_USER_NAME="${1}"
                        GIT_REPO_NAME="${2}"
                        FILE_PATH="${3}"
                        GITHUB_TOKEN="${4}"

                        content_decoded=$(curl -s -H "Authorization: token ${GITHUB_TOKEN}" \
                            "https://raw.githubusercontent.com/${GIT_USER_NAME}/${GIT_REPO_NAME}/main/${FILE_PATH}")

                        current_tag=$(echo "$content_decoded" | grep -o 'image: [^ ]*' | sed 's/image: //' | grep -o '[0-9]\\+\\.[0-9]')

                        major=0; minor=0
                        if [[ $current_tag =~ ([0-9]+)\\.([0-9]+) ]]; then
                            major=${BASH_REMATCH[1]}
                            minor=${BASH_REMATCH[2]}
                        fi
                        if [ "$minor" -ge 9 ]; then
                            major=$((major + 1))
                            minor=0
                        else
                            minor=$((minor + 1))
                        fi

                        new_tag="${major}.${minor}"
                        echo "$new_tag"
                    '''
                    
                    sh 'chmod +x get_version.sh'

                    withCredentials([string(credentialsId: 'github', variable: 'GITHUB_TOKEN')]) {
                        env.IMAGE_TAG = sh(
                            script: "./get_version.sh ${GIT_USER_NAME} ${GIT_REPO_NAME} ${DEPLOYMENT_FILE} ${GITHUB_TOKEN}",
                            returnStdout: true
                        ).trim()
                    }
                    env.DOCKER_IMAGE = "${DOCKER_USERNAME}/${REPO_NAME}:${env.IMAGE_TAG}"
                }
            }
        }
        stage('Setup SCM and Environment') {
            steps {
                checkout scm
                sh '''
                    curl -sSL https://install.python-poetry.org | python3 -
                    export PATH="$HOME/.local/bin:$PATH"
                '''
                sh 'poetry --version'
            }
        }
        stage('Export Requirements') {
            steps {
                sh 'export PATH="$HOME/.local/bin:$PATH" && poetry export -f requirements.txt --output requirements.txt --without-hashes'
            }
        }
        stage('Build and Push Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh "echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }
        stage('Update Deployment File') {
            steps {
                withCredentials([string(credentialsId: 'github', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                        set -e
                        rm -rf ${GIT_REPO_NAME} || true
                        git clone https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_REPO_NAME}.git
                        cd ${GIT_REPO_NAME}
                        git config user.email "${GIT_USER_EMAIL}"
                        git config user.name "${GIT_USER_NAME}"
                        git pull origin main
                        sed -i "s|image: ${DOCKER_USERNAME}/${REPO_NAME}:[^ ]*|image: ${DOCKER_USERNAME}/${REPO_NAME}:${IMAGE_TAG}|g" ${DEPLOYMENT_FILE}
                        git add ${DEPLOYMENT_FILE}
                        git commit -m "Update deployment image to version ${IMAGE_TAG} [Jenkins build ${IMAGE_TAG}]"
                        git push https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_REPO_NAME}.git HEAD:main
                    '''
                }
            }
        }
    }
    post {
        always {
            echo 'Cleaning up workspace...'
        }
        success {
            echo "Pipeline succeeded! New Docker image: ${DOCKER_IMAGE}"
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
