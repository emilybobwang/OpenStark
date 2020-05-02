import request from '../utils/request';

export async function query() {
  return request('/api/py/users');
}

export async function queryCurrent() {
  return request('/api/py/user/currentUser');
}

export async function editCurrent(params) {
  return request('/api/py/user/currentUser', {
    method: 'POST',
    body: params,
  });
}

export async function register(params) {
  return request('/api/py/register', {
    method: 'POST',
    body: params,
  });
}

export async function accountLogin(params) {
  return request('/api/py/login', {
    method: 'POST',
    body: params,
  });
}

export async function accountAutoLogin() {
  return request('/api/py/autoLogin', {
    method: 'POST',
  });
}

export async function accountLogout() {
  return request('/api/py/logout');
}

export async function sendActiveMail() {
  return request('/api/py/activeUser', {
    method: 'POST',
  });
}
