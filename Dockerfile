# Muse & AI 视频专业提示词工坊 - 轻量生产级 Docker 镜像
FROM nginx:alpine

# 拷贝静态资源与自定义 Nginx 配置
COPY index.html /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
