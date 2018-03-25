# https://www.packer.io/docs/builders/docker.html#basic-example-changes-to-metadata
from packerlicious import builder, Ref, Template, UserVar

builders = [
    builder.Docker(
        image="ubuntu",
        commit=True,
        changes=[
            "USER www-data",
            "WORKDIR /var/www",
            "ENV HOSTNAME www.example.com",
            "VOLUME /test1 /test2",
            "EXPOSE 80 443",
            "LABEL version=1.0",
            "ONBUILD RUN date",
            "CMD [\"nginx\", \"-g\", \"daemon off;\"]",
            "ENTRYPOINT /var/www/start.sh"
        ]
    )
]


t = Template()
t.add_builder(builders)

print(t.to_json())
