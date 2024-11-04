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

        // ... other stages (Build Docker Image, Push Docker Image, etc.)
    }

    post {
        always {
            script {
                // Error handling for cleanup actions
                try {
                    sh 'docker rmi rafin1998/rafin-blog-site:0.7 || true'
                    sh 'rm requirements.txt || true'
                } catch (Exception e) {
                    echo 'Cleanup failed: ' + e.getMessage()
                }
            }
        }
    }
}
