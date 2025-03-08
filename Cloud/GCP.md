## Google Cloud Secret Manager

```
gcloud secrets create API_KEY_NAME --replication-policy=automatic

echo -n "your-api-key-value" | gcloud secrets versions add API_KEY_NAME --data-file=-
```

```
gcloud secrets versions access latest --secret=API_KEY_NAME
```

