#  Copyright (c) 2020 - 2023, Arm Limited. All rights reserved.<BR>
class PatchCheckConf:
    ignore_change_id = False
    ignore_multi_package = False

        if mo.group(3) == 'devel@edk2.groups.io':
            self.error("Email rewritten by lists DMARC / DKIM / SPF: " +
                       email)

        if ' via groups.io' in name.lower() and mo.group(3).endswith('@groups.io'):
        self.ignore_multi_package = False
            if not PatchCheckConf.ignore_change_id:
                self.check_change_id_format()
            self.check_ci_options_format()
            self.ok &= EmailAddressCheck(s[3], sig).ok
        for sigtype in self.sig_types:
            sigs = self.find_signatures(sigtype)
    def check_change_id_format(self):
        cid='Change-Id:'
        if self.msg.find(cid) != -1:
            self.error('\"%s\" found in commit message:' % cid)
            return

    def check_ci_options_format(self):
        cio='Continuous-integration-options:'
        for line in self.msg.splitlines():
            if not line.startswith(cio):
                continue
            options = line.split(':', 1)[1].split()
            if 'PatchCheck.ignore-multi-package' in options:
                self.ignore_multi_package = True

                if self.filename.endswith('.rtf'):
                    self.force_crlf = False
                    self.force_notabs = False
                   os.path.basename(self.filename).lower() == 'makefile' or \
                   os.path.splitext(self.filename)[1] == '.makefile' or \
                   self.filename.startswith(
                        'BaseTools/Source/C/VfrCompile/Pccts/'):
            if self.binary or self.filename.endswith(".rtf"):
        rp_file = os.path.realpath(self.filename)
        rp_script = os.path.realpath(__file__)
        if line.find('__FUNCTION__') != -1 and rp_file != rp_script:
            self.added_line_error('__FUNCTION__ was used, but __func__ '
                                  'is now recommended', line)

        self.ignore_multi_package = msg_check.ignore_multi_package
        dec_files = self.read_dec_files_from_git()
            check_patch = CheckOnePatch(commit, patch)
            self.ok &= check_patch.ok
            ignore_multi_package = check_patch.ignore_multi_package
            if PatchCheckConf.ignore_multi_package:
                ignore_multi_package = True
            prefix = 'WARNING: ' if ignore_multi_package else ''
            check_parent = self.check_parent_packages (dec_files, commit, prefix)
            if not ignore_multi_package:
                self.ok &= check_parent

    def check_parent_packages(self, dec_files, commit, prefix):
        ok = True
        modified = self.get_parent_packages (dec_files, commit, 'AM')
        if len (modified) > 1:
            print("{}The commit adds/modifies files in multiple packages:".format(prefix))
            print(" *", '\n * '.join(modified))
            ok = False
        deleted = self.get_parent_packages (dec_files, commit, 'D')
        if len (deleted) > 1:
            print("{}The commit deletes files from multiple packages:".format(prefix))
            print(" *", '\n * '.join(deleted))
            ok = False
        return ok

    def get_parent_packages(self, dec_files, commit, filter):
        filelist = self.read_files_modified_from_git (commit, filter)
        parents = set()
        for file in filelist:
            dec_found = False
            for dec_file in dec_files:
                if os.path.commonpath([dec_file, file]):
                    dec_found = True
                    parents.add(dec_file)
            if not dec_found and os.path.dirname (file):
                # No DEC file found and file is in a subdir
                # Covers BaseTools, .github, .azurepipelines, .pytool
                parents.add(file.split('/')[0])
        return list(parents)

    def read_dec_files_from_git(self):
        # run git ls-files *.dec
        out = self.run_git('ls-files', '*.dec')
        # return list of .dec files
        try:
            return out.split()
        except:
            return []

    def read_files_modified_from_git(self, commit, filter):
        # run git diff-tree --no-commit-id --name-only -r <commit>
        out = self.run_git('diff-tree', '--no-commit-id', '--name-only',
                           '--diff-filter=' + filter, '-r', commit)
        try:
            return out.split()
        except:
            return []

        group.add_argument("--ignore-change-id",
                           action="store_true",
                           help="Ignore the presence of 'Change-Id:' tags in commit message")
        group.add_argument("--ignore-multi-package",
                           action="store_true",
                           help="Ignore if commit modifies files in multiple packages")
        if self.args.ignore_change_id:
            PatchCheckConf.ignore_change_id = True
        if self.args.ignore_multi_package:
            PatchCheckConf.ignore_multi_package = True