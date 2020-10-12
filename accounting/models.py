from django.db import models
from django.utils.translation import gettext as _
from .apps import APP_NAME
from django.shortcuts import reverse
from app.settings import ADMIN_URL

class FinancialDocumentCategory(models.Model):
    title=models.CharField(_("دسته بندی سند های مالی"), max_length=50)

    

    class Meta:
        verbose_name = _("FinancialDocumentCategory")
        verbose_name_plural = _("دسته بندی های سند های مالی")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("CurrentFeeCategory_detail", kwargs={"pk": self.pk})


class FinancialDocument(models.Model):    
    financial_year=models.ForeignKey("FinancialYear", verbose_name=_("سال مالی"), on_delete=models.PROTECT)
    title=models.CharField(_("عنوان"), max_length=50)
    category=models.ForeignKey("FinancialDocumentCategory",null=True, verbose_name=_("دسته بندی"), on_delete=models.PROTECT)
    amount=models.IntegerField(_("مبلغ"))
    date_added=models.DateTimeField(_("تاریخ ثبت"), auto_now=False, auto_now_add=True)
    date_edited=models.DateTimeField(_("تاریخ ویرایش"), auto_now=True, auto_now_add=False)
    date_document=models.DateTimeField(_("تاریخ سند"), auto_now=False, auto_now_add=False)
    links=models.ManyToManyField("app.Link", verbose_name=_("لینک ها"),blank=True)
    documents=models.ManyToManyField("app.Document", verbose_name=_("فایل ها"),blank=True)
    child_class=models.CharField(_("child_class"), max_length=50,blank=True)
    class Meta:
        verbose_name = _("FinancialDocument")
        verbose_name_plural = _("اسناد مالی")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("accounting:financial_document", kwargs={"financial_document_id": self.pk})

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/financialdocument/{self.pk}/change/'

class FinancialYear(models.Model):
    title=models.CharField(_("عنوان"), max_length=50)
    year=models.IntegerField(_("سال مالی"),default=1399)
    # documents=models.ManyToManyField("FinancialDocument", blank=True,verbose_name=_("اسناد مالی"))


    class Meta:
        verbose_name = _("FinancialYear")
        verbose_name_plural = _("سال های مالی")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("accounting:financial_year", kwargs={"financial_year_id": self.pk})


class FinancialAccount(models.Model):
    title=models.CharField(_("عنوان"), max_length=50)
    
    class Meta:
        verbose_name = _("FinancialAccount")
        verbose_name_plural = _("حساب های مالی")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("accounting:financial_account", kwargs={"financial_account_id": self.pk})


class FinancialTransaction(FinancialDocument):
    from_account=models.ForeignKey("FinancialAccount",related_name="from_account", verbose_name=_("از"), on_delete=models.PROTECT)
    to_account=models.ForeignKey("FinancialAccount", verbose_name=_("به"), related_name="to_account",on_delete=models.PROTECT)
    


    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/financialtransaction/{self.pk}/change/'

    class Meta:
        verbose_name = _("FinancialTransaction")
        verbose_name_plural = _("تراکنش های مالی")

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("FinancialAccount_detail", kwargs={"pk": self.pk})

    def save(self):
        self.child_class='financialtransaction'
        super(FinancialTransaction,self).save()

class FinancialProfile(FinancialAccount):
    profile=models.ForeignKey("app.Profile", verbose_name=_("پروفایل"), on_delete=models.PROTECT)
    bank_accounts=models.ManyToManyField("BankAccount",blank=True, verbose_name=_("حساب های بانکی"))


    class Meta:
        verbose_name = _("FinancialProfile")
        verbose_name_plural = _("پروفایل های مالی")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("accounting:financial_profile", kwargs={"financial_profile_id": self.pk})


class Cash(FinancialAccount):

    

    class Meta:
        verbose_name = _("Cash")
        verbose_name_plural = _("صندوق ها")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Cash_detail", kwargs={"pk": self.pk})


class BankAccount(models.Model):
    owner=models.ForeignKey("app.Profile", verbose_name=_("صاحب حساب"), null=True,blank=True,on_delete=models.PROTECT)
    bank=models.ForeignKey("Bank", verbose_name=_("بانک"), on_delete=models.CASCADE)
    account_no=models.CharField(_("شماره حساب"), null=True,blank=True,max_length=50)
    card_no=models.CharField(_("شماره کارت"), null=True,blank=True,max_length=50)
    shaba_no=models.CharField(_("شماره شبا"), null=True,blank=True,max_length=50)
    class Meta:
        verbose_name = _("BankAccount")
        verbose_name_plural = _("حساب های بانکی")

    def __str__(self):
        return f'حساب {self.bank.name} {self.owner.name()}'

    def get_absolute_url(self):
        return reverse("BankAccount_detail", kwargs={"pk": self.pk})


class Bank(models.Model):
    name=models.CharField(_("نام بانک"), max_length=50)
    branch=models.CharField(_("شعبه"), max_length=50)
    

    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("بانک ها")

    def __str__(self):
        return f'بانک {self.name} شعبه {self.branch}'

    def get_absolute_url(self):
        return reverse("Bank_detail", kwargs={"pk": self.pk})


class CurrentFeeCategory(models.Model):
    title=models.CharField(_("دسته بندی هزینه های جاری"), max_length=50)

    

    class Meta:
        verbose_name = _("CurrentFeeCategory")
        verbose_name_plural = _("دسته بندی های هزینه های جاری")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("CurrentFeeCategory_detail", kwargs={"pk": self.pk})


class CurrentFee(FinancialDocument):
    fee_category=models.ForeignKey("CurrentFeeCategory", verbose_name=_("دسته بندی هزینه های جاری"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = _("CurrentFee")
        verbose_name_plural = _("هزینه های جاری")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("CurrentFee_detail", kwargs={"pk": self.pk})

