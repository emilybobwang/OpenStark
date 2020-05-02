import { stringify } from 'qs';
import request from '../utils/request';

export async function getGuiTest(op, action, params) {
  return request(`/api/py/test/gui/${op}/${action}?${stringify(params)}`);
}

export async function editGuiTest(op, action, params) {
  return request(`/api/py/test/gui/${op}/${action}`, {
    method: 'POST',
    body: params,
  });
}

export async function getApiTest(op, action, params) {
  return request(`/api/py/test/api/${op}/${action}?${stringify(params)}`);
}

export async function editApiTest(op, action, params) {
  return request(`/api/py/test/api/${op}/${action}`, {
    method: 'POST',
    body: params,
  });
}
