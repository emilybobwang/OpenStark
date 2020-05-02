import { stringify } from 'qs';
import request from '../utils/request';

export async function queryNotices(params) {
  return request(`/api/py/user/notices?${stringify(params)}`);
}

export async function getCommonInfo() {
  return request('/api/py/getCommonInfo');
}

export async function clearNotices(params) {
  return request('/api/py/user/notices', {
    method: 'POST',
    body: params,
  });
}

export async function sendMail(op, params) {
  return request(`/api/py/mail/${op}`, {
    method: 'POST',
    body: params,
  });
}
