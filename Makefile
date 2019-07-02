# Silly hack to generate a semi-random bucket name based on
# the local hostname
SUFFIX := $(shell hostname | md5sum | cut -c1-10 )
S3_BUCKET := oidc-idp-stack-$(SUFFIX)

OIDC_THUMBPRINT := EEACBD0CB452819577911E1E6203DB262F84A318

all: package deploy

bucket:
	if ! aws s3api head-bucket --bucket $(S3_BUCKET); then \
		aws s3 mb s3://$(S3_BUCKET); \
	fi

package: cloudformation/oidc-idp-and-role.yml bucket
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

.PHONY: package deploy bucket
