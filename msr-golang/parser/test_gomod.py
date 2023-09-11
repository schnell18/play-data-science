import unittest
from gomod import GoMod


class GoModTest(unittest.TestCase):

    tc_require_replace = """
// This is a generated file. Do not edit directly.

module k8s.io/kube-proxy

go 1.20

require github.com/beorn7/perks v1.0.1
require github.com/blang/semver/v4 v4.0.0 // indirect

require (
	k8s.io/apimachinery v0.28.1
	k8s.io/component-base v0.28.1
)

require (
	github.com/cespare/xxhash/v2 v2.2.0 // indirect
	github.com/go-logr/logr v1.2.4 // indirect
	github.com/gogo/protobuf v1.3.2 // indirect
	github.com/golang/protobuf v1.5.3 // indirect
	github.com/google/go-cmp v0.5.9 // indirect
	github.com/google/gofuzz v1.2.0 // indirect
	github.com/inconshreveable/mousetrap v1.1.0 // indirect
	github.com/json-iterator/go v1.1.12 // indirect
	github.com/kr/text v0.2.0 // indirect
	github.com/matttproud/golang_protobuf_extensions v1.0.4 // indirect
	github.com/modern-go/concurrent v0.0.0-20180306012644-bacd9c7ef1dd // indirect
	github.com/modern-go/reflect2 v1.0.2 // indirect
	github.com/prometheus/client_golang v1.16.0 // indirect
	github.com/prometheus/client_model v0.4.0 // indirect
	github.com/prometheus/common v0.44.0 // indirect
	github.com/prometheus/procfs v0.10.1 // indirect
	github.com/spf13/cobra v1.7.0 // indirect
	github.com/spf13/pflag v1.0.5 // indirect
	golang.org/x/net v0.13.0 // indirect
	golang.org/x/sys v0.10.0 // indirect
	golang.org/x/text v0.11.0 // indirect
	google.golang.org/protobuf v1.30.0 // indirect
	gopkg.in/inf.v0 v0.9.1 // indirect
	gopkg.in/yaml.v2 v2.4.0 // indirect
	k8s.io/klog/v2 v2.100.1 // indirect
	k8s.io/utils v0.0.0-20230406110748-d93618cff8a2 // indirect
	sigs.k8s.io/json v0.0.0-20221116044647-bc3834ca7abd // indirect
	sigs.k8s.io/structured-merge-diff/v4 v4.2.3 // indirect
	sigs.k8s.io/yaml v1.3.0 // indirect
)

replace (
	// k8s.io/api => k8s.io/api v0.28.0
	k8s.io/api => k8s.io/api v0.28.1
	k8s.io/apimachinery => k8s.io/apimachinery v0.28.1
	k8s.io/client-go => k8s.io/client-go v0.28.1
	k8s.io/component-base => k8s.io/component-base v0.28.1
    golang.org/x/net v1.2.3 => ./fork/net
    golang.org/x/net => ./fork/net

)
"""

    tc_require_with_comment = """
module github.com/vshn/k8up

go 1.15

require (
	// When updating crd-ref-docs, verify that there were no changes from Elastic to hostile licenses.
	github.com/elastic/crd-ref-docs v0.0.7
	github.com/go-logr/logr v0.4.0
	github.com/go-logr/zapr v0.4.0
	github.com/imdario/mergo v0.3.11
	github.com/knadh/koanf v0.15.0
	github.com/prometheus/client_golang v1.9.0
	github.com/robfig/cron/v3 v3.0.1
	github.com/stretchr/testify v1.7.0
	go.uber.org/zap v1.16.0
	k8s.io/api v0.20.4
	k8s.io/apimachinery v0.20.4
	k8s.io/client-go v0.20.4
	k8s.io/utils v0.0.0-20210111153108-fddb29f9d009
	sigs.k8s.io/controller-runtime v0.8.2
	sigs.k8s.io/controller-tools v0.5.0
	sigs.k8s.io/kustomize/kustomize/v3 v3.8.7
)
"""

    tc_require_with_comment_in_the_middle = """
module github.com/metal-stack/metal-hammer

require (
	github.com/beevik/ntp v0.3.0
	github.com/dsnet/compress v0.0.1 // indirect
	github.com/fatih/color v1.9.0 // indirect
	github.com/frankban/quicktest v1.10.0 // indirect
	github.com/go-openapi/errors v0.19.6
	github.com/go-openapi/runtime v0.19.21
	github.com/go-openapi/strfmt v0.19.5
	github.com/go-openapi/swag v0.19.9
	github.com/go-openapi/validate v0.19.10
	github.com/google/gopacket v1.1.17
	github.com/google/uuid v1.1.2
	github.com/inconshreveable/log15 v0.0.0-20200109203555-b30bc20e4fd1
	github.com/jaypipes/ghw v0.6.0
	github.com/mattn/go-runewidth v0.0.9 // indirect
	github.com/mdlayher/ethernet v0.0.0-20190606142754-0394541c37b7
	github.com/mdlayher/lldp v0.0.0-20150915211757-afd9f83164c5
	github.com/mdlayher/raw v0.0.0-20191009151244-50f2db8cc065
	github.com/metal-stack/go-hal v0.1.10
	github.com/metal-stack/metal-api v0.8.2
	github.com/metal-stack/metal-lib v0.6.3
	github.com/metal-stack/v v1.0.2
	// archiver must stay in version v2.1.0, see replace below
	github.com/mholt/archiver v3.1.1+incompatible
	github.com/nwaples/rardecode v1.1.0 // indirect
	github.com/pierrec/lz4 v2.5.2+incompatible
	github.com/pkg/errors v0.9.1
	github.com/stretchr/testify v1.6.1
	github.com/u-root/u-root v6.0.0+incompatible
	github.com/vishvananda/netlink v1.0.0
	github.com/vishvananda/netns v0.0.0-20191106174202-0a2b9b5464df // indirect
	golang.org/x/sys v0.0.0-20200803210538-64077c9b5642
	google.golang.org/grpc v1.31.0
	gopkg.in/cheggaaa/pb.v1 v1.0.28
	gopkg.in/yaml.v2 v2.3.0
)

replace github.com/mholt/archiver => github.com/mholt/archiver v2.1.0+incompatible

go 1.13
    """

    def testRequireAndReplace(self):
         mod = GoMod(GoModTest.tc_require_replace)
         self.assertEqual(mod.go_version, "1.20")
         self.assertEqual(mod.module_path, "k8s.io/kube-proxy")
         self.assertTrue(mod.replaces is not None)
         self.assertEqual(len(mod.replaces), 6)
         self.assertEqual(mod.replaces[0].left.module, "k8s.io/api")
         self.assertEqual(mod.replaces[0].left.version, "")
         self.assertEqual(mod.replaces[0].right.module, "k8s.io/api")
         self.assertEqual(mod.replaces[0].right.version, "v0.28.1")
         self.assertEqual(mod.replaces[5].left.module, "golang.org/x/net")
         self.assertEqual(mod.replaces[5].left.version, "")
         self.assertEqual(mod.replaces[5].right.module, "./fork/net")
         self.assertEqual(mod.replaces[5].right.version, "")
         self.assertTrue(mod.requires is not None)
         self.assertEqual(len(mod.requires), 33)
         self.assertEqual(mod.requires[0].module, "github.com/beorn7/perks")
         self.assertEqual(mod.requires[0].version, "v1.0.1")
         self.assertFalse(mod.requires[0].indirect)
         self.assertEqual(mod.requires[1].module, "github.com/blang/semver/v4")
         self.assertEqual(mod.requires[1].version, "v4.0.0")
         self.assertTrue(mod.requires[1].indirect)


    def testRequireWithComment(self):
         mod = GoMod(GoModTest.tc_require_with_comment)
         self.assertEqual(mod.go_version, "1.15")
         self.assertEqual(mod.module_path, "github.com/vshn/k8up")
         self.assertTrue(mod.replaces is not None)
         self.assertTrue(len(mod.replaces) == 0)
         self.assertTrue(mod.requires is not None)
         self.assertEqual(len(mod.requires), 16)
         self.assertEqual(mod.requires[0].module, "github.com/elastic/crd-ref-docs")
         self.assertEqual(mod.requires[0].version, "v0.0.7")
         self.assertFalse(mod.requires[0].indirect)
         self.assertEqual(mod.requires[1].module, "github.com/go-logr/logr")
         self.assertEqual(mod.requires[1].version, "v0.4.0")
         self.assertFalse(mod.requires[1].indirect)

    def testRequireWithCommentInTheMiddle(self):
         mod = GoMod(GoModTest.tc_require_with_comment_in_the_middle)
         self.assertEqual(mod.go_version, "1.13")
         self.assertEqual(mod.module_path, "github.com/metal-stack/metal-hammer")
         self.assertTrue(mod.replaces is not None)
         self.assertTrue(len(mod.replaces) == 1)
         self.assertEqual(mod.replaces[0].left.module, "github.com/mholt/archiver")
         self.assertEqual(mod.replaces[0].left.version, "")
         self.assertEqual(mod.replaces[0].right.module, "github.com/mholt/archiver")
         self.assertEqual(mod.replaces[0].right.version, "v2.1.0+incompatible")
         self.assertTrue(mod.requires is not None)
         self.assertEqual(len(mod.requires), 33)
         self.assertEqual(mod.requires[0].module, "github.com/beevik/ntp")
         self.assertEqual(mod.requires[0].version, "v0.3.0")
         self.assertFalse(mod.requires[0].indirect)
         self.assertEqual(mod.requires[21].module, "github.com/mholt/archiver")
         self.assertEqual(mod.requires[21].version, "v3.1.1+incompatible")
         self.assertFalse(mod.requires[21].indirect)
         self.assertEqual(mod.requires[28].module, "github.com/vishvananda/netns")
         self.assertEqual(mod.requires[28].version, "v0.0.0-20191106174202-0a2b9b5464df")
         self.assertTrue(mod.requires[28].indirect)


if __name__ == "__main__":
    # run the test
    unittest.main()
