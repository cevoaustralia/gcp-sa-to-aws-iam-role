S3_BUCKET := cmp-stupid-inflation
OIDC_THUMBPRINT := abcd1234567890abcd1234567890abcd12345678

all: package deploy

package: cloudformation/oidc-idp-and-role.yml
	aws cloudformation package \
		--template-file $< \
		--s3-bucket $(S3_BUCKET) \
		--output-template-file rendered.yml

deploy: package
	aws cloudformation deploy \
		--template-file rendered.yml \
		--stack-name oidc-idp-and-role \
		--parameter-overrides OIDCThumbprint=$(OIDC_THUMBPRINT) OIDCAudiences=$(CLIENT_ID) \
		--capabilities CAPABILITY_NAMED_IAM

clean:
	rm -f rendered.yml

.PHONY: package deploy

