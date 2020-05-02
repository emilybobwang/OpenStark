import React, { PureComponent } from 'react';
import { connect } from 'dva';
import { Divider, Popconfirm, BackTop } from 'antd';
import Router from 'umi/router';
import { EditorState } from 'braft-editor';
import ReactMarkdown from 'react-markdown';
import styles from '../../Tools/style.less';

@connect(({ knowledge, user }) => ({
  knowledge,
  currentUser: user.currentUser,
}))
class Blog extends PureComponent {
  componentDidMount() {
    const {
      dispatch,
      match: { params },
    } = this.props;
    if (params.bid !== '0') {
      dispatch({
        type: 'knowledge/getBooks',
        op: 'book',
        action: 'single',
        payload: { bid: params.bid },
      });
    }
  }

  handleDelete = key => {
    const {
      match: { params },
      dispatch,
    } = this.props;
    dispatch({
      type: 'knowledge/editBooks',
      payload: {
        key,
      },
      op: 'book',
      action: 'delete',
      callback: ()=>{
        Router.push(`/knowledge/books/blog/${params.cid}`);
      },
    });
  };

  getViewDom = ref => {
    this.view = ref;
  };

  render() {
    const {
      knowledge: { blogContent, bookCate },
      currentUser,
    } = this.props;
    const cate = bookCate.filter(item => item.id === (blogContent.cid && blogContent.cid[0]));
    return (
      <div className={styles.baseView} ref={this.getViewDom}>
        <div className={styles.left}>
          <div>
            分类:{' '}
            {cate.length < 1
              ? '未分类'
              : cate.map(item =>
                  item.name
                    .concat(' / ')
                    .concat(
                      item.child
                        .filter(ele => ele.id === (blogContent.cid && blogContent.cid[1]))
                        .map(e => e.name) || '其他'
                    )
                )}{' '}
            <Divider type="vertical" /> 作者: {blogContent.author} <Divider type="vertical" />{' '}
            发布日期: {blogContent.publishTime} <Divider type="vertical" /> 更新日期:{' '}
            {blogContent.updateTime} <Divider type="vertical" />{' '}
            <a href="/knowledge/books/edit/NEW_TEMP_KEY">新增知识</a>{' '}
            {blogContent.bid &&
            (currentUser.userId === blogContent.uid || currentUser.authority === 'admin') ? (
              <span>
                <Divider type="vertical" />{' '}
                <a href={`/knowledge/books/edit/${blogContent.bid}`}>编辑</a>{' '}
                <Divider type="vertical" />{' '}
                <Popconfirm
                  title="确定要删除？"
                  onConfirm={() => {
                    this.handleDelete(blogContent.bid || 0);
                  }}
                >
                  <a>删除</a>
                </Popconfirm>
              </span>
            ) : (
              ''
            )}
          </div>
          <Divider />
          <ReactMarkdown
            source={
              blogContent.type === 'html'
                ? EditorState.createFrom(blogContent.blog).toHTML()
                : blogContent.blog
            }
            className={styles.blogContent}
            escapeHtml={false}
          />
          <BackTop />
        </div>
      </div>
    );
  }
}

export default Blog;
