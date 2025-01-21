export function isLogged(){
    return localStorage.getItem('user-id');
}

export function saveSession(userId: string) {
    localStorage.setItem('user-id', userId);
}

export function deleteSession() {
    localStorage.removeItem('user-id');
}

export function getUserId(): string {
    return localStorage.getItem('user-id')
}