import React, { PureComponent, Fragment } from 'react';
import { Form, Input, Button, Row, Col, Card, Popconfirm, Icon, Alert } from 'antd';
import Link from 'umi/link';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';

const FormItem = Form.Item;
const { Search } = Input;

@connect(({ user, knowledge, loading }) => ({
  currentUser: user.currentUser,
  knowledge,
  loading: loading.effects['knowledge/editBooks'],
  fetchLoading: loading.effects['knowledge/getBooks'],
}))
@Form.create()
class Books extends PureComponent {
  state = {
    isDelete: false,
    keyWords: '',
  };

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'knowledge/getBooks',
      op: 'cate',
      action: 'list',
    });
  }

  handleSubmit = e => {
    const { form, dispatch } = this.props;
    e.preventDefault();
    form.validateFields({ force: true }, (err, values) => {
      if (!err) {
        dispatch({
          type: 'knowledge/editBooks',
          payload: {
            ...values,
          },
          op: 'cate',
          action: 'add',
          callback:()=>{
            dispatch({
              type: 'knowledge/getBooks',
              op: 'cate',
              action: 'list',
            });
          },
        });
      }
    });
  };

  handleDelete = key => {
    const { dispatch } = this.props;
    dispatch({
      type: 'knowledge/editBooks',
      payload: {
        cid: key,
      },
      op: 'cate',
      action: 'delete',
      callback: ()=>{
        dispatch({
          type: 'knowledge/getBooks',
          op: 'cate',
          action: 'list',
        });
      },
    });
  };

  onSearch = filter => {
    const { dispatch } = this.props;
    const keyWords = typeof filter === 'string' ? filter : filter.target.value;
    dispatch({
      type: 'knowledge/getBooks',
      op: 'book',
      action: 'search',
      payload: {
        keyWords,
      },
    });
    this.setState({
      keyWords,
    });
  };

  render() {
    const {
      form: { getFieldDecorator },
      fetchLoading,
      loading,
      knowledge: { bookCate, blogList },
      currentUser,
    } = this.props;
    const { isDelete, keyWords } = this.state;
    const addCate = (
      <Form onSubmit={this.handleSubmit} hideRequiredMark layout="inline">
        <FormItem>
          <Button icon="plus" type="primary" href="/knowledge/books/edit/NEW_TEMP_KEY">
            新增知识
          </Button>
        </FormItem>
        <FormItem required>
          {getFieldDecorator('cateOne', {
            rules: [{ required: true, message: '请输入一级分类' }],
          })(<Input autoFocus placeholder="一级分类" />)}
        </FormItem>
        <FormItem required>
          {getFieldDecorator('cateTwo', {
            rules: [{ required: true, message: '请输入二级分类' }],
          })(<Input placeholder="二级分类" />)}
        </FormItem>
        <FormItem>
          <Button icon="save" type="primary" loading={loading} htmlType="submit">
            保存
          </Button>
        </FormItem>
        <FormItem>
          <Button
            type="danger"
            icon={isDelete ? 'undo' : 'delete'}
            onClick={() => {
              this.setState({ isDelete: !isDelete });
            }}
          >
            {isDelete ? '取消' : '删除'}
          </Button>
        </FormItem>
      </Form>
    );

    const cateList = bookCate.map(item => (
      <Col span={4} key={item.id} style={{ minHeight: 200 }}>
        <h2>
          {item.id !== 0 ? (
            item.name
          ) : (
            <Link to={`/knowledge/books/blog/${item.id}`}>{item.name}</Link>
          )}{' '}
          {isDelete && item.id !== 0 && (
            <Popconfirm
              title="确定要删除？"
              onConfirm={() => {
                this.handleDelete(item.id);
              }}
            >
              <a>
                <Icon type="delete" />
              </a>
            </Popconfirm>
          )}
        </h2>
        <ul style={{ fontSize: 16 }}>
          {item.child.map(ele => (
            <li key={ele.id}>
              <Link to={`/knowledge/books/blog/${ele.id}`}>{ele.name}</Link>{' '}
              {isDelete && ele.id !== 0 && (
                <Popconfirm
                  title="确定要删除？"
                  onConfirm={() => {
                    this.handleDelete(ele.id);
                  }}
                >
                  <a>
                    <Icon type="delete" />
                  </a>
                </Popconfirm>
              )}
            </li>
          ))}
        </ul>
      </Col>
    ));

    const bookList =
      blogList.length > 0 ? (
        blogList.map(item => (
          <Col span={12} key={item.id}>
            <ul style={{ fontSize: 16 }}>
              <li key={item.id}>
                <Link target="_blank" to={`/knowledge/books/blog/${item.cid}/${item.id}`}>
                  {item.title}
                </Link>
                <span style={{ fontSize: 8 }}>
                  &nbsp;&nbsp;(作者: {item.author}&nbsp;&nbsp;&nbsp;&nbsp;更新时间:{' '}
                  {item.updateTime})
                </span>
              </li>
            </ul>
          </Col>
        ))
      ) : (
        <Alert message="相关知识未储备!" type="warning" />
      );

    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card
            bordered={false}
            loading={fetchLoading}
            title={
              <Search
                style={{ maxWidth: 300 }}
                placeholder="按标题/内容/作者搜索"
                onSearch={this.onSearch}
                onChange={this.onSearch}
                enterButton
                autoFocus
              />
            }
            extra={
              currentUser.authority === 'admin' ? (
                addCate
              ) : (
                <Form onSubmit={this.handleSubmit} hideRequiredMark layout="inline">
                  <FormItem>
                    <Button icon="plus" type="primary" href="/knowledge/books/edit/NEW_TEMP_KEY">
                      新增知识
                    </Button>
                  </FormItem>
                  <FormItem required>
                    {getFieldDecorator('cateOne', {
                      rules: [{ required: true, message: '请输入一级分类' }],
                    })(<Input placeholder="一级分类" />)}
                  </FormItem>
                  <FormItem required>
                    {getFieldDecorator('cateTwo', {
                      rules: [{ required: true, message: '请输入二级分类' }],
                    })(<Input placeholder="二级分类" />)}
                  </FormItem>
                  <FormItem>
                    <Button type="primary" icon="save" loading={loading} htmlType="submit">
                      保存
                    </Button>
                  </FormItem>
                </Form>
              )
            }
          >
            <Row>{keyWords.trim() === '' ? cateList : bookList}</Row>
          </Card>
        </Fragment>
      </PageHeaderWrapper>
    );
  }
}

export default Books;
